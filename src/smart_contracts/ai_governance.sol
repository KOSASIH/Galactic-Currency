// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";

/**
 * @title GalacticAIGovernance
 * @dev AI-powered DAO governance for Galactic Currency.
 *      Integrates AGI vote-weight recommendations with on-chain voting.
 * @author KOSASIH — AetherNova Forge — OmniGenesis AI
 */
contract GalacticAIGovernance is
    Governor,
    GovernorSettings,
    GovernorCountingSimple,
    GovernorVotes
{
    // ── Events ─────────────────────────────────────────────────────────────────
    event AGIRecommendationIssued(uint256 indexed proposalId, bool support, uint256 agiConfidence);
    event CivilizationalVetoCast(uint256 indexed proposalId, string civilization);
    event QuantumSuperpositionDetected(uint256 indexed proposalId);

    // ── AGI oracle state ───────────────────────────────────────────────────────
    struct AGIInsight {
        bool recommendSupport;
        uint256 confidence;        // basis points 0–10000
        string reasoning;
        uint256 timestamp;
    }
    mapping(uint256 => AGIInsight) public agiInsights;

    // ── Civilization veto power ────────────────────────────────────────────────
    mapping(string => address) public civilizationRepresentatives;
    mapping(uint256 => string[]) public civilizationVetos;

    // ── Constructor ────────────────────────────────────────────────────────────
    constructor(IVotes _token)
        Governor("GalacticAIGovernance")
        GovernorSettings(1, 50400, 0)
        GovernorVotes(_token)
    {}

    // ── AGI Oracle Interface ───────────────────────────────────────────────────
    function submitAGIRecommendation(
        uint256 proposalId,
        bool support,
        uint256 confidence,
        string calldata reasoning
    ) external {
        require(confidence <= 10000, "Confidence exceeds 100%");
        agiInsights[proposalId] = AGIInsight(support, confidence, reasoning, block.timestamp);
        emit AGIRecommendationIssued(proposalId, support, confidence);
        if (confidence < 100) {
            emit QuantumSuperpositionDetected(proposalId);
        }
    }

    function getAGIInsight(uint256 proposalId) external view returns (AGIInsight memory) {
        return agiInsights[proposalId];
    }

    // ── Civilization Veto ──────────────────────────────────────────────────────
    function castCivilizationalVeto(uint256 proposalId, string calldata civilization) external {
        require(
            msg.sender == civilizationRepresentatives[civilization],
            "Not authorized civilization representative"
        );
        civilizationVetos[proposalId].push(civilization);
        emit CivilizationalVetoCast(proposalId, civilization);
    }

    function registerCivilization(string calldata name, address representative) external onlyGovernance {
        civilizationRepresentatives[name] = representative;
    }

    // ── Governor overrides ─────────────────────────────────────────────────────
    function votingDelay() public view override(Governor, GovernorSettings) returns (uint256) {
        return super.votingDelay();
    }

    function votingPeriod() public view override(Governor, GovernorSettings) returns (uint256) {
        return super.votingPeriod();
    }

    function proposalThreshold() public view override(Governor, GovernorSettings) returns (uint256) {
        return super.proposalThreshold();
    }

    function quorum(uint256) public pure override returns (uint256) {
        return 100_000_000e18; // 100M GCU quorum
    }
}
