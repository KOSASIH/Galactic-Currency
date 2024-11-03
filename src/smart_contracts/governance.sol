// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/governance/utils/Snapshotting.sol";

contract Governance is Ownable {
    using SafeMath for uint256;

    IERC20 public token;

    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 totalVotes;
        uint256 votingDeadline;
        bool executed;
        mapping(address => bool) voters;
    }

    Proposal[] public proposals;
    uint256 public quorum; // Minimum votes required for a proposal to pass

    event ProposalCreated(uint256 proposalId, string description, uint256 votingDeadline);
    event Voted(uint256 proposalId, address voter, uint256 votes);
    event ProposalExecuted(uint256 proposalId);

    constructor(IERC20 _token, uint256 _quorum) {
        token = _token;
        quorum = _quorum;
    }

    function createProposal(string memory description, uint256 votingPeriod) public onlyOwner {
        uint256 votingDeadline = block.timestamp + votingPeriod;

        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            totalVotes: 0,
            votingDeadline: votingDeadline,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, description, votingDeadline);
    }

    function vote(uint256 proposalId) public {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(block.timestamp < proposals[proposalId].votingDeadline, "Voting period has ended");
        require(!proposals[proposalId].voters[msg.sender], "You have already voted");

        uint256 votes = token.balanceOf(msg.sender);
        require(votes > 0, "No voting power");

        proposals[proposalId].voters[msg.sender] = true;
        proposals[proposalId].voteCount = proposals[proposalId].voteCount.add(votes);
        proposals[proposalId].totalVotes = proposals[proposalId].totalVotes.add(votes);

        emit Voted(proposalId, msg.sender, votes);
    }

    function executeProposal(uint256 proposalId) public onlyOwner {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(block.timestamp >= proposals[proposalId].votingDeadline, "Voting period has not ended");
        require(!proposals[proposalId].executed, "Proposal already executed");
        require(proposals[proposalId].voteCount >= quorum, "Not enough votes to execute");

        // Here you can add logic to execute the proposal
        proposals[proposalId].executed = true;

        emit ProposalExecuted(proposalId);
    }

    function updateQuorum(uint256 newQuorum) external onlyOwner {
        quorum = newQuorum;
    }

    function getProposal(uint256 proposalId) external view returns (string memory description, uint256 voteCount, uint256 totalVotes, uint256 votingDeadline, bool executed) {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        return (proposal.description, proposal.voteCount, proposal.totalVotes, proposal.votingDeadline, proposal.executed);
    }
}
