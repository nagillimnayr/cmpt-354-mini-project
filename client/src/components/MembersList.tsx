import {
  Table,
  TableHead,
  TableRow,
  Paper,
  TableContainer,
  TableBody,
  TableCell,
} from '@mui/material';
import Member from '../model/Member';
import { useCallback, useEffect, useState } from 'react';
import { SERVER_URL } from '../common/constants';

type MemberData = Omit<Member, 'dateOfBirth'> & {
  dateOfBirth: string;
};

const MembersList = () => {
  const [members, setMembers] = useState<Member[]>([]);

  const fetchMembers = useCallback(async () => {
    const url = `${SERVER_URL}/members`;
    const response = await fetch(url, {
      method: 'GET',
    });
    const data = await response.json();
    setMembers(
      data.map(({ dateOfBirth, ...obj }: MemberData) => {
        const member: Member = {
          ...obj,
          dateOfBirth: new Date(dateOfBirth),
        };
        return member;
      })
    );
  }, []);

  useEffect(() => {
    fetchMembers();
  }, [fetchMembers]);

  return (
    <TableContainer
      component={Paper}
      sx={{ width: '100%' }}
    >
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>First Name</TableCell>
            <TableCell>Last Name</TableCell>
            <TableCell>Date of Birth</TableCell>
            <TableCell>Phone Number</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {members.map((member) => (
            <TableRow key={member.memberId}>
              <TableCell align='right'>{member.memberId}</TableCell>
              <TableCell align='right'>{member.firstName}</TableCell>
              <TableCell align='right'>{member.lastName}</TableCell>
              <TableCell align='right'>
                {member.dateOfBirth.toUTCString()}
              </TableCell>
              <TableCell align='right'>{member.phoneNumber}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default MembersList;
